from django.urls import path

from women import views


urlpatterns = [
    path('', views. WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),

    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),

    path('category/<slug:cat_slug>/',
         views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
]
