import json
import logging

from django.shortcuts import render, redirect
from chat.utils.canvas_client import get_canvas_client
from django.http import JsonResponse
from django.core.serializers import serialize
from django.conf import settings
from django.urls import reverse

# llm imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from chat.models import Course, CourseFile, Conversation, Message



def login(request):
    return render(request, "login.html")


def load_canvas_course_files(request):
    canvas_client = get_canvas_client(request.user)
    course_reponse = canvas_client.courses()

    if course_reponse:
        courses = course_reponse.json()

        for course in courses:
            course_obj, _ = Course.objects.update_or_create(
                user=request.user, 
                external_id=course["id"],
                defaults={
                    "name": course["name"],
                }
            )

            course_files_response = canvas_client.course_files(course["id"])
            if course_files_response:
                for file in course_files_response.json():
                    course_file, _ = CourseFile.objects.update_or_create(
                        course=course_obj,
                        external_id=file["id"],
                        defaults={
                            "name": file["display_name"],
                            "url": file["url"],
                        }
                    )
    return JsonResponse({})


def tokenize_selected_files(request):
    chat_id = request.GET.get("chat_id")
    file_ids = request.GET.get('file_ids')
    
    if isinstance(file_ids, str):
        file_ids = [int(id) for id in file_ids.split(",")]

    files = CourseFile.objects.filter(id__in=file_ids)

    if not files:
        return JsonResponse({"error": "Files not available"}, status=400)

    for file in files:
        if not file.pages:
            file.generate_pages()

        file.refresh_from_db()
        if not file.pages:
            continue
    
    if chat_id in ["new", None]:
        chat = Conversation.objects.create(
            user=request.user,
            title="temp_title"
        )
    else:
        chat  = Conversation.objects.get(id=int(chat_id))
    
    chat.build_index_with_course_files(files)
    return JsonResponse({"response": "index building complete"})


def chat_interface(request):
    chats = Conversation.objects.filter(user=request.user).values("id", "title")
    courses = Course.objects.prefetch_related('coursefile_set').filter(user=request.user).all()

    course_files = []

    for course in courses:
        course_dict = {
            "course_id": course.id,
            "course_name": course.name,
            "files": []
        }

        for file in course.coursefile_set.all():
            course_dict["files"].append(
                {
                    "id": file.id,
                    "name": file.name,
                    "url": file.url
                }
            )

        course_files.append(course_dict)

    context = {
        "chats": chats,
        "chat_messages": [],
        "course_files": course_files,
        "current_chat_id": None
    }
    return render(request, "chatbox.html", context=context)


def chat_detail(request, chat_id):
    all_chats = Conversation.objects.filter(user=request.user).values("id", "title")
    current_chat = Conversation.objects.get(id=chat_id) #TODO make better
    courses = Course.objects.prefetch_related('coursefile_set').filter(user=request.user).all()

    messages = [{'text': msg.text, "is_human": msg.is_human} for msg in current_chat.message_set.order_by('id')]

    course_files = []

    for course in courses:
        course_dict = {
            "course_id": course.id,
            "course_name": course.name,
            "files": []
        }

        for file in course.coursefile_set.all():
            course_dict["files"].append(
                {
                    "id": file.id,
                    "name": file.name,
                    "url": file.url
                }
            )

        course_files.append(course_dict)

    context = {
        "chats": all_chats,
        "chat_messages": messages,
        "course_files": course_files,
        "current_chat_id": current_chat.id
    }
    return render(request, "chatbox.html", context=context)


def get_chatbot_response(request):
    chat_id = request.GET.get("chat_id")
    user_input = request.GET.get("input_message")

    if not user_input:
        return JsonResponse({"error": "missing user input"}, status=400)
    
    if not chat_id:
        chat = Conversation.objects.create(
            user=request.user,
            title="fresh chat created"
        )
    else:
        chat = Conversation.objects.get(id=chat_id)
    
    #save user input
    Message.objects.create(conversation=chat, text=user_input, is_human=True)

    vector  = None
    chat_history = None

    if chat.vector_index:
        vector = chat.get_vector_index()

    if chat.message_set.exists():
        chat_history = [
            HumanMessage(content=msg.text) if msg.is_human else \
                AIMessage(content=msg.text) for msg in chat.message_set.order_by('id')
        ]

    retriever = None
    if vector:
        retriever = vector.as_retriever()


    # CONVERSATION RETRIEVAL CHAIN
    llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY)

    # First we need a prompt that we can pass into an LLM to generate this search query
    if retriever:
        retriever_prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            ("user", "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
        ])
        retriever_chain = create_history_aware_retriever(llm, retriever, retriever_prompt)

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer the user's questions based on the below context:\n\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])

    if retriever:
        chat_chain = create_stuff_documents_chain(llm, chat_prompt)
        
        query_chain = create_retrieval_chain(retriever_chain, chat_chain)

        query_response = query_chain.invoke({
                "chat_history": chat_history,
                "input": user_input
            })
        response = query_response["answer"]
        
    else:
        chat_prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])

        query_chain = chat_prompt | llm 
        query_response = query_chain.invoke({
                "chat_history": chat_history,
                "input": user_input
            })
        response = query_response.content

    if response:
         #save AI response
        Message.objects.create(conversation=chat, text=response, is_human=False)

        if not chat_id:
            return JsonResponse(
                {
                    "response": response,
                    "redirect": reverse("chat_detail", kwargs={"chat_id": chat.id})
                })

        return JsonResponse({'response': response})
    return JsonResponse({"response": "Sorry, Your AI is quite today"})


def new_chat(request):
    chat = Conversation.objects.create(
        user=request.user,
        title="new_chat_temp_name"
    )

    return redirect('chat_detail', chat_id=chat.id)
