#!/bin/bash


# Run the Tailwind CSS build command
npx tailwindcss -i ./app/static/src/input.css -o ./app/static/css/output.css --watch
