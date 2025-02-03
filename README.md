# CS417SRProject

## Run Instructions:

1) cd into the "Frontend" folder.
2) run "npm run dev".

backend

1) cd backend
2) python3 -m venv venv
3) source venv/bin/activate (mac) | venv\Scripts\activate (pc)
5) pip install -r requirements.txt


## Notes for Devs

Vue Router is already installed in this application.

If you are going to make adjustments, I think the only things you have to edit are in the /src and /public folders.

    /assets has aesthetics stuff, like logos and css stylesheets
    /components has the FUNCTIONAL aesthetics stuff. Specifically, templates that we can reference across pages.
    /router has the code for page navigation. Might have to be updated periodically with new pages being added.
    /views has the actual pages. Add them as required and then we can just call the code to navigate pages (I think)

Do not touch anything else (I think)

If you are developing and want to see your updates in real-time, run
```
npm run dev 
```
in your Terminal. Any updates you save to the program will update in real time which is pretty neat.


## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).
See [Vite Configuration Reference](https://vite.dev/config/).

