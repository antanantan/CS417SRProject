Things to Do! Listed in Order of Priority

User Profile
  - create user profile and store information in a database. users need to be able to log in and out of the application.
  - allow user to create allergen profile and store information in a database. ensure that the allergen information is unique for each user.

Allergen Profile
  - import menu information into the menu interface **(Y)**
  - get allergen profile to filter 

Location Information
  - allow map page to accept geographical information from device and display that information. **(E)**

Miscellaneous
  - remedy security issues as indicated on github!
  - fix disclaimer not closing for some reason **(A)**


E's Notes
  - can confirm that data is being passed upon creating an account and logging in via console log, and i changed the routing in the front and backend to transfer to the profile, but regardless of whether an account is associated or not, the website will still proceed with bringing the user to the profile page, despite exceptions being listed in the backend. i have no idea how to fix this though
  - we have to figure out how to use axios to pass HTTP requests from vue into flask
  - update (1/29): it's a little bit messy (the map is gone from the location view because i'm trying to get the form to work with the backend) but you can still access the page, nothing is visually missing it's just the functionality that's absent