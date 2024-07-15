;; Auto-generated. Do not edit!


(when (boundp 'my_serial_node::Balance)
  (if (not (find-package "MY_SERIAL_NODE"))
    (make-package "MY_SERIAL_NODE"))
  (shadow 'Balance (find-package "MY_SERIAL_NODE")))
(unless (find-package "MY_SERIAL_NODE::BALANCE")
  (make-package "MY_SERIAL_NODE::BALANCE"))

(in-package "ROS")
;;//! \htmlinclude Balance.msg.html


(defclass my_serial_node::Balance
  :super ros::object
  :slots (_weight ))

(defmethod my_serial_node::Balance
  (:init
   (&key
    ((:weight __weight) 0.0)
    )
   (send-super :init)
   (setq _weight (float __weight))
   self)
  (:weight
   (&optional __weight)
   (if __weight (setq _weight __weight)) _weight)
  (:serialization-length
   ()
   (+
    ;; float64 _weight
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _weight
       (sys::poke _weight (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _weight
     (setq _weight (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get my_serial_node::Balance :md5sum-) "41998f6691705e7d3db1ca4195275ab0")
(setf (get my_serial_node::Balance :datatype-) "my_serial_node/Balance")
(setf (get my_serial_node::Balance :definition-)
      "float64 weight
")



(provide :my_serial_node/Balance "41998f6691705e7d3db1ca4195275ab0")


