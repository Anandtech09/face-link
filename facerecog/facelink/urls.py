from django.urls import path
from .import views

urlpatterns=[
    path('', views.contact),
    path('signup', views.signup,name="signup"),
    path('profile<str:pk>', views.show, name="profile"),
    path('showall',views.view1),
    path('delete<str:pk>',views.delete,name="delete"),
    path('login',views.login,name="login"),
    path('main',views.main),
    path('second',views.second),
    path('faculty-signup', views.fac_signup),
    path('faculty-login', views.faclogin),
    path('exit/',views.getout,name='exit'),
    path('contact',views.contact),
    path('profile',views.profile),
    path('twoprofile',views.twoprofile),
    path('teachupdate<str:pk>', views.tea_update, name="teachupdate"),
    path('update<str:lm>', views.update, name="update"),
    path('details',views.details),
    path('biodata',views.biodata),
    path('face-recognition', views.face_recognition, name='face-recognition'),
    path('failure', views.failure, name='failure'),
    path('generate_pdf',views.generate_pdf,name="generate_pdf"),
    path('scholarship_list',views.scholarship_list),
    path('present<str:pk>', views.present, name="present"),
    path('overall',views.overall_attendance),
]
