from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required

def index(request):
    products = Listing.objects.all()
    empty = False
    
    if not len(products):
        empty = True
    
    return render(request, "auctions/index.html", {
            "products": products,
            "empty": empty
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    return render(request, "auctions/categories.html")

def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user.username)
    empty = True
    products = []

    if watchlist:
        empty = False
        for product in watchlist:
            products.append(Listing.objects.get(id=product.listingid))

    return render(request, "auctions/watchlist.html", {
        "products": products,
        "empty": empty,
    })

def createListing(request):
    return render(request, "auctions/createListing.html")

def submit(request):
    if request.method == "POST":
        item = Listing()
        item.owner = request.user.username
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.startBid = request.POST.get('bid')
        item.category = request.POST.get('category')
        if request.POST.get('url'):
            item.link = request.POST.get('url')
        else:
            item.link = "https://icon-library.com/icon/no-photo-available-icon-8.html"
        item.save()

        products = Listing.objects.all()
        empty = False
        if not len(products):
            empty = True

        return render(request, "auctions/index.html", {
            "products": products,
            "empty": empty
        })

def category(request, ctg):
    if ctg  == "road":
        products = Listing.objects.filter(category="Road Bike")
        bike = "Road Bikes"
    if ctg  == "mountain":
        products = Listing.objects.filter(category="Mountain Bike")    
        bike = "Mountain Bikes"
    if ctg  == "gravel":
        products = Listing.objects.filter(category="Gravel Bike")
        bike = "Gravel Bikes"
    if ctg  == "fixie-singlespeed":
        products = Listing.objects.filter(category="Fixie/Single speed Bike")
        bike = "Fixie/Single speed Bikes"

    empty = False
    if not len(products):
        empty = True

    return render(request, "auctions/category.html", {
        "products": products,
        "empty": empty,
        "bike": bike
    })

@login_required(login_url='/login')
def viewListing(request, id):

    comments = Comment.objects.filter(listingid=id)
    product = Listing.objects.get(id=id)

    if request.method == "POST":
        newbid = request.POST.get("bid")
        oldbid = product.startBid

        if int(newbid) > oldbid:
            product.startBid = newbid
            product.save()

            bidobj = Bid.objects.filter(listingid=id)
            if bidobj:
                bidobj.delete()

            obj = Bid()
            obj.user = request.user.username
            obj.title = product.title
            obj.listingid = id
            obj.bid = newbid
            obj.save()

            product = Listing.objects.get(id=id)

            return render(request, "auctions/listing.html", {
                "product": product,
                "comments": comments,
                "message": "Your bid is added.",
                "placed": True
            })
        else:
            product = Listing.objects.get(id=id)

            return render(request, "auctions/listing.html", {
                "product": product,
                "comments": comments,
                "message": "Your bid should be higher than the previous one.",
                "placed": False
            })
    else:
        product = Listing.objects.get(id=id)
        watchlist = Watchlist.objects.filter(listingid=id, user=request.user.username)
        winners = Winner.objects.filter(listingid=id)

        onwatchlist = False
        won = False
        owner = False
        closed = False
    
        if watchlist:
            onwatchlist = True
            
        if winners:
            closed = True
            if request.user.username == winners.first().winner:
                won = True
        else:
            if request.user.username == product.owner:
                owner = True

        return render(request, "auctions/listing.html", {
            "product": product,
            "comments": comments,
            "onwatchlist": onwatchlist,
            "won": won,
            "owner": owner,
            "closed": closed
        })

def addWatchlist(request, id):
    added = Watchlist()
    added.user = request.user.username
    added.listingid = id
    added.save()

    watchlist = Watchlist.objects.filter(user=request.user.username)
    empty = True
    products = []

    if watchlist:
        empty = False
        for product in watchlist:
            products.append(Listing.objects.get(id=product.listingid))

    return render(request, "auctions/watchlist.html", {
        "products": products,
        "empty": empty,
        "message": "Product is added to your watchlist"
    })

def removeWatchlist(request, id):
    Watchlist.objects.get(listingid=id, user=request.user.username).delete()
    watchlist = Watchlist.objects.filter(user=request.user.username)
    empty = True
    products = []

    if watchlist:
        empty = False
        for product in watchlist:
            products.append(Listing.objects.get(id=product.listingid)) 
        
    return render(request, "auctions/watchlist.html", {
        "products": products,
        "empty": empty,
        "message": "Product is removed from your watchlist"
    })

def closeListing(request, id):
    winner = Winner()
    bids = Bid.objects.filter(listingid=id)
    comments = Comment.objects.filter(listingid=id)

    if bids:
        bid = bids.first()
        winner.owner = request.user.username
        winner.winner = bid.user
        winner.listingid = id
        winner.winprice = bid.bid
        winner.save()

        return render(request, "auctions/listing.html", {
            "product": Listing.objects.get(id=id),
            "comments": comments,
            "closed": True
        })

def addComment(request, id):
    comment = Comment()
    comment.user = request.user.username
    comment.comment = request.POST.get("comment")
    comment.listingid = id
    comment.save()
    
    comments = Comment.objects.filter(listingid=id)
    
    return render(request, "auctions/listing.html", {
        "product": Listing.objects.get(id=id),
        "comments": comments,
        "closed": False
    })

    