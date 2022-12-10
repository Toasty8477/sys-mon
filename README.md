# Sys-mon System Monitor

## What?

Sys-mon is a lightweight, containerized system monitor written in python that can be used on all versions of linux.

## Why?

I was using a similar system monitor program that ran as a service to output performance stats to [Home Assistant](https://home-assistant.io). For a while it worked but it was only able to run on debian based systems. I decided to make a similar prgram but running in docker so it could run across different types of linux distros.

## How?

Run the provided docker-compose.yaml with `docker compose up -d` and docker should pull the correct image.
