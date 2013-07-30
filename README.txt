==============
AdenCf Commons
==============

Application Django inter-projets FigaroClassifieds
==================================================


Git How-to
----------


push de la branche master sur origin::

    git push origin master

Pour *tracker* automatiquement origin/master avec la copie locale de master::

    git branch --set-upstream master origin/master
    git pull/push # plus besoin de préciser origin master.

Annoted tag::

    git tag -a v1.0 -m"Version 1.0"
    git push origin v1.0

commit::

    git -am"New stuff."

Branches::

    git branch ticket-1
    git checkout ticket-1
    commit etc..
    
    git checkout master
    git merge ticket-1

    git branch -d ticket-1


Faire une copie locale d'une remote branche : il faut la créer localement (?)
http://git-scm.com/book/en/Git-Branching-Remote-Branches#Pushing
::

    git checkout -b serverfix origin/serverfix


