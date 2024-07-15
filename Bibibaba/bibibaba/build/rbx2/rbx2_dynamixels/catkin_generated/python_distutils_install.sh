#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/bibibaba/bibibaba/src/rbx2/rbx2_dynamixels"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/bibibaba/bibibaba/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/bibibaba/bibibaba/install/lib/python3/dist-packages:/home/bibibaba/bibibaba/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/bibibaba/bibibaba/build" \
    "/usr/bin/python3" \
    "/home/bibibaba/bibibaba/src/rbx2/rbx2_dynamixels/setup.py" \
     \
    build --build-base "/home/bibibaba/bibibaba/build/rbx2/rbx2_dynamixels" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/bibibaba/bibibaba/install" --install-scripts="/home/bibibaba/bibibaba/install/bin"
