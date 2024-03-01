# LOREKEEPER #

## Overview

Lorekeeper is the answer to a problem I've personally had with managing dungeons and dragons campaigns. As such it has many roles to fill of its own.

When I looked for solutions to manage the lore behind my campaigns, I could never find something that was simple enough to use on they fly, but also complex enough to hold all the pertiant information. I tried mind maps, word documents, and many other solutions but none filled the role I needed.

Then it hit me. SQL. PostgreSQL is a near infinite tool to make and link data. Not just that, but PostgreSQL is n-dimentional.

Lorekeeper is in its infancy, but as they say "it works on my machine"

Humor aside, more details are to follow...

# Back End

## Actors

Actors are any character, from player, to POV to NPC.


Here's the scema for Actors:

```pgsql
id SERIAL PRIMARY KEY,
first_name TEXT,
middle_name TEXT,
last_name TEXT,
title TEXT,
actor_age INT,
class_id INT,
actor_level INT,
background_id INT,
job TEXT,
actor_role TEXT,
race_id INT,
sub_race_id INT,
alignment VARCHAR(2),
strength INT,
dexterity INT,
constitution INT,
intelligence INT,
wisdom INT,
charisma INT,
ideal TEXT,
bond TEXT,
flaw TEXT,
appearance TEXT,
strengths TEXT,
weaknesses TEXT,
notes TEXT,

FOREIGN KEY (class_id) REFERENCES classes(id),
FOREIGN KEY (background_id) REFERENCES background(id),
FOREIGN KEY (race_id) REFERENCES race(id),
FOREIGN KEY (sub_race_id) REFERENCES sub_race(id)
```


**_Let's break it down one element at a time:_**

### id
As any ID in PostgreSQL, this one is auto generated.
### first_name
First Name of the Actor
#### Note: first_name will be used for Proper Name (shortened version)
### middle_name
Middle Name of the Actor (can be blank)
### last_name
Last Name of the Actor
### title
Things like Dr., Arch Mage, that kind of thing.
### actor_age
How old the Actor is.
### class_id
ID (as int) of class found in the class list.
### actor_level
INT of the character's level overall.
### background_id
ID (as int) of Background found in the Backgrounds table
### job
What job does this Actor do? Are they homeless? A Blacksmith?
### actor_role
Why is this character in your story? Are they a villian? Sidekick?
### race_id
ID (as int) of the characters Race found in race table
### sub_race_id
ID (as int) of a sub race (if any)
### alignment
2 letter code to represent alignment and disposition.

CG NG LG

CN NN LN

CE NE LE

### strength
Int (typically out of 20) to represent Actor's Strength. (10=Default)
### dexterity
Int (typically out of 20) to represent Actor's Dexterity (10=Default)
### constitution
Int (typically out of 20) to represent Actor's Constitution (10=Default)
### intelligence
Int (typically out of 20) to represent Actor's Intelligence (10=Default)
### wisdom
Int (typically out of 20) to represent Actor's Wisdom (10=Default)
### charisma
Int (typically out of 20) to represent Actor's Charisma (10=Default)
### ideal
A text description of what ideals the Actor strives for. Kindness, Equality, Power, that sort of thing.
### bond
A text description of something that the Actor cares a great deal for. Person, place, Thing, w/e.
### flaw
A text description of a specific flaw the Actor has. Something that usually can be exploited.
### appearance
A text description of what the Actor looks like. As long as needed.
### strengths
A text description of what the Actor is good at. As long as needed.
### weaknesses
A text description of what the Actor struggles with. What they are bad at. As long as needed.
### notes
A place for any additional notes not covered previously.


Lorekeeper is primarally a DND tool at the moment so some of the traits tracked are specific to DND.

