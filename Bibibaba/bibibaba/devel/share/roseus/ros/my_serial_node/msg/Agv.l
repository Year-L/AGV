;; Auto-generated. Do not edit!


(when (boundp 'my_serial_node::Agv)
  (if (not (find-package "MY_SERIAL_NODE"))
    (make-package "MY_SERIAL_NODE"))
  (shadow 'Agv (find-package "MY_SERIAL_NODE")))
(unless (find-package "MY_SERIAL_NODE::AGV")
  (make-package "MY_SERIAL_NODE::AGV"))

(in-package "ROS")
;;//! \htmlinclude Agv.msg.html


(defclass my_serial_node::Agv
  :super ros::object
  :slots (_power ))

(defmethod my_serial_node::Agv
  (:init
   (&key
    ((:power __power) 0.0)
    )
   (send-super :init)
   (setq _power (float __power))
   self)
  (:power
   (&optional __power)
   (if __power (setq _power __power)) _power)
  (:serialization-length
   ()
   (+
    ;; float64 _power
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _power
       (sys::poke _power (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _power
     (setq _power (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get my_serial_node::Agv :md5sum-) "b61bda1d4e0075084b2082bebb59ea34")
(setf (get my_serial_node::Agv :datatype-) "my_serial_node/Agv")
(setf (get my_serial_node::Agv :definition-)
      "float64 power


")



(provide :my_serial_node/Agv "b61bda1d4e0075084b2082bebb59ea34")


