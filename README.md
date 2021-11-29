# netlist 
## v.0.0 - 11/28
netlist, a tag based network cli app. python regret

this app allows you to set tags for individuals, store information for them, and then read that information at scale. It's a great organizing tool that measures how long it's bene since you last talked with someoneone.

recommendations:
- be picky about tags you have --> try to minimize them
- app works best when try to give each person 1 tag. Networks should be focused anways!
- embrace the tag and organize feature to it's max
- explore how to configure the template.json to add in your own custom configurations

## key workflows
- run `netlist add` to add a user to your network. You will be prompted for paramters pulled from `db/template.json` and some mandatory params. Will automatically - - store `timePinged` to track how long since you interacted with this user
- run `netlist read` to read any user's information
- run `netlist ping` to ping a user and reset their `timePinged` variable
- run `netlist list` to list all users in the db sorted by `timePinged` (most recent to least recent). Can also list by tag 
- run `netlist summary` to get a summary of all tags and the top users in each tag. Helps track how healthy & balanced your network is
