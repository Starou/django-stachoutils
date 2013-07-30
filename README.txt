==============
AdenCf Commons
==============

GIT
'''

# push de la branche master sur origin.
git push origin master

# Annoted tag.
git tag -a v1.0 -m"Version 1.0"
git push origin v1.0

# commit.
git -am"New stuff."

# branches
git branch ticket-1
git checkout ticket-1
commit etc..
git checkout master
git merge ticket-1

git branch -d ticket-1
