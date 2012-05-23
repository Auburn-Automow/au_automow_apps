function _roscomplete_rosapp {
    COMPREPLY=()
    arg="${COMP_WORDS[COMP_CWORD]}"

    if [[ $COMP_CWORD == 1 ]]; then
        opts="list info start stop"
        COMPREPLY=($(compgen -W "$opts" -- ${arg}))
    elif [[ $COMP_CWORD == 2 ]]; then
        case ${COMP_WORDS[1]} in
            list)
                opts=`~/devel/ros/au_automow_apps/automow_apps/scripts/rosapp.py list -ar 2> /dev/null`
                COMPREPLY=($(compgen -W "$opts" -- ${arg}))                
                ;;
            start)
                opts=`~/devel/ros/au_automow_apps/automow_apps/scripts/rosapp.py list -a 2> /dev/null`
                COMPREPLY=($(compgen -W "$opts" -- ${arg}))
                ;;
            stop)
                opts=`~/devel/ros/au_automow_apps/automow_apps/scripts/rosapp.py list -r 2> /dev/null`
                COMPREPLY=($(compgen -W "$opts" -- ${arg}))
                ;;
        esac
    fi

}

complete -F "_roscomplete_rosapp" "rosapp.py"
