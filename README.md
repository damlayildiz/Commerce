# Commerce

This is a simple website for auction sales. 

## Features 
-   **Create Listing Page** where users can specify a title for the listing, a description, and the starting bid. Users can also provide a URL of an image and a category.
-   **Active Listings Page** where users can view all of the currently active auction listings.
-   **Listing Page**: Users can view all details about the listing, including the current price for the listing. Additionally, If the user is signed in, user;
     -   can add/remove the item to/from their *Watchlist.* 
    -    can bid on the item. The bid must be greater than any other bids and the starting bid. If the bid doesn’t meet these criteria, the user is presented with an error.
    -  can add or view comments to/on the listing page. 
    -   If the user is the one who created the listing, the user can close the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
    -   On a closed listing page, if the user has won that auction, the page indicates that.
 
-   **Watchlist** which displays all of the listings that a user has added to their watchlist. 
-   **Categories Page** displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.
-   **Django Admin Interface**: Via the Django admin interface, a site administrator can view, add, edit, and delete any listings, comments, and bids made on the website.

## Screenshots and Demo
  ![Screenshot from 2021-03-14 00-26-14](https://user-images.githubusercontent.com/56313500/111046690-de387900-845d-11eb-9c90-7c8963989f3e.png)
---
  ![Screenshot from 2021-03-14 00-26-16](https://user-images.githubusercontent.com/56313500/111046766-e395c380-845d-11eb-9cda-87cf1ab69cd7.png)
---
  ![Screenshot from 2021-03-14 00-26-20](https://user-images.githubusercontent.com/56313500/111046828-e85a7780-845d-11eb-962d-a4e99162b808.png)
---
  ![Screenshot from 2021-03-14 00-26-26](https://user-images.githubusercontent.com/56313500/111046896-ed1f2b80-845d-11eb-80e0-a127901eedb9.png)

[Youtube Demo Link](https://youtu.be/SF8uUJcl69s)

## Run Search locally

### Step 1: Clone project
```
 git clone https://github.com/damlayildiz/Commerce.git
 cd Commerce 
 ```
### Step 2: Run the project
```
 python manage.py runserver
 ```
