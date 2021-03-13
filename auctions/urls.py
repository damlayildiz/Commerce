from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("createListing", views.createListing, name="createListing"),
    path("submit", views.submit, name="submit"),
    path("category/<str:ctg>", views.category, name="category"),
    path("viewListing/<int:id>", views.viewListing, name="viewListing"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing"),
    path("addComment/<int:id>", views.addComment, name="addComment")
    
]
