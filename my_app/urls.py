

from django.contrib import admin
from django.urls import path, include

from my_app import views

from django.urls import path
urlpatterns = [
    path('',views.login),
    path('view_expert',views.view_expert),
    path('home',views.home),
    path('login_post',views.login_post),
    path('view_users',views.view_users),
    path('send_notifications',views.send_notifications),
    path('view_complaints',views.view_complaints),
    path('view_feedback',views.view_feedback),
    path('logout',views.logout),
    path('signup_user',views.signup_user),
    path('signup_expert',views.signup_expert),
    path('user_reg',views.user_reg),
    path('user_reg_post',views.user_reg_post),
    path('expert_reg',views.expert_reg),
    path('expert_reg_post',views.expert_reg_post),
    path('user_home',views.user_home),
    path('admin_home',views.admin_home),
    # user
    path('send_complaints',views.send_complaints),
    path('send_feedback',views.send_feedback),
    path('chatwithuser',views.chatwithuser),
    path('send_complaints_post',views.send_complaints_post),


path('chatwithuser', views.chatwithuser, name='chatwithuser'),
path('chatview', views.chatview, name='chatview'),
path('coun_msg/<int:id>', views.coun_msg, name='coun_msg'),
path('coun_insert_chat/<str:msg>/<int:id>', views.coun_insert_chat, name='coun_insert_chat'),

path('chatwithetouser', views.chatwithetouser, name='chatwithetouser'),
path('chatviewExpert', views.chatviewExpert, name='chatviewExpert'),
path('coun_insert_chatExpert/<str:msg>/<int:id>/', views.coun_insert_chatExpert, name='coun_insert_chatExpert'),
path('coun_msgExpert/<int:id>', views.coun_msgExpert, name='coun_msgExpert'),



path('experthome' , views.experthome),
path('ex_send_notifications' , views.ex_send_notifications),
path('view_user_req' , views.view_user_req),
path('view_adm_notifications' , views.view_adm_notifications),
path('user_view_notifications' , views.user_view_notifications),
path('send_reply/<id>' , views.send_reply),
path('block_user/<id>' , views.block_user),
path('unblock_user/<id>' , views.unblock_user),
path('accept_expert/<id>' , views.accept_expert),
path('reject_expert/<id>' , views.reject_expert),
path('delete_complaints/<id>' , views.delete_complaints),
path('send_reply_post' , views.send_reply_post),
path('send_feedback_post' , views.send_feedback_post),
path('manage_dataset' , views.manage_dataset),
path('pred_input' , views.pred_input),
path('ex_send_notifications_post' , views.ex_send_notifications_post),
path('pred_input_post' , views.pred_input_post),
path('view_result' , views.view_result),
path('chat_with_expert2' , views.chat_with_expert2),
path('send_notification_post' , views.send_notification_post),
path('view_dataset', views.view_dataset),
path('insert_data', views.insert_data),
path('expert_home', views.expert_home),
path('forgot_psw', views.forgot_psw),
path('forgot_psw_post', views.forgot_psw_post),
path('delete_expert/<id>', views.delete_expert),
path('admin_dashboard', views.admin_dashboard),






]

