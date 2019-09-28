#!/bin/bash
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

# start docker
if ! [ `systemctl is-active docker` = "active" ]; then
    sudo systemctl start docker
fi

# terminal
SESSIONNAME="C3S"
tmux has-session -t $SESSIONNAME &> /dev/null
if [ $? != 0 ]; then
  tmux new-session -s $SESSIONNAME -n docker -c . -d
  tmux send-keys -t $SESSIONNAME "docker-compose up" C-m
  tmux new-window -a -t $SESSIONNAME -n docker -c .
  tmux send-keys -t $SESSIONNAME "git status" C-m
  tmux new-window -a -t $SESSIONNAME -n collecting_society -c ./shared/src/collecting_society
  tmux send-keys -t $SESSIONNAME "git status" C-m
  tmux new-window -a -t $SESSIONNAME -n portal -c ./shared/src/collecting_society.portal
  tmux send-keys -t $SESSIONNAME "git status" C-m
  tmux new-window -a -t $SESSIONNAME -n repertoire -c ./shared/src/collecting_society.portal.repertoire
  tmux send-keys -t $SESSIONNAME "git status" C-m
  tmux select-window -t $SESSIONNAME:docker
fi

# start firefox after waiting till docker containers have been started
sleep 10
firefox https://redmine.c3s.cc/login http://repertoire.test:81 &

tmux attach -t $SESSIONNAME
