![alt tag](https://raw.githubusercontent.com/scorchio/teamstars/feature-drupal-import/teamstars/static/img/teamstars_logo.png)


# TeamStars: a Django pet project

In small, non-formal communities there's often a need for sending positive 
feedback to each other, possibly in a way which is visible to everyone else 
in the community. There are many benefits:

- since in such small communities there are virtually no "reward", the 
emphasized positive feedback can help the organizers a lot and avoids getting
 them burned out
- sending positive feedback promotes good actions and reinforces the right 
patterns of action
- based on the activity, you can easily get metrics about the community's 
"health" (= how active it is, who are the most active people, who cares to 
send the most feedback and so on).

This project gives a Django implementation for a dedicated site where 
people could send votes for others, rewarding the work the other one did for 
them.

*This is a minimalist work-in-progress; as such, a lot of features that you 
might expect are not there yet.*
 
## Future

- A fully usable REST API so one could easily write a mobile client as a 
frontend (the current feature set is already available via Django REST 
Framework)
- Statistics dashboard (only a basic leaderboard is implemented yet)
- E-mail notifications
