; Auto-generated. Do not edit!


(cl:in-package my_serial_node-msg)


;//! \htmlinclude Agv.msg.html

(cl:defclass <Agv> (roslisp-msg-protocol:ros-message)
  ((power
    :reader power
    :initarg :power
    :type cl:float
    :initform 0.0))
)

(cl:defclass Agv (<Agv>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Agv>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Agv)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name my_serial_node-msg:<Agv> is deprecated: use my_serial_node-msg:Agv instead.")))

(cl:ensure-generic-function 'power-val :lambda-list '(m))
(cl:defmethod power-val ((m <Agv>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_serial_node-msg:power-val is deprecated.  Use my_serial_node-msg:power instead.")
  (power m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Agv>) ostream)
  "Serializes a message object of type '<Agv>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'power))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Agv>) istream)
  "Deserializes a message object of type '<Agv>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'power) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Agv>)))
  "Returns string type for a message object of type '<Agv>"
  "my_serial_node/Agv")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Agv)))
  "Returns string type for a message object of type 'Agv"
  "my_serial_node/Agv")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Agv>)))
  "Returns md5sum for a message object of type '<Agv>"
  "b61bda1d4e0075084b2082bebb59ea34")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Agv)))
  "Returns md5sum for a message object of type 'Agv"
  "b61bda1d4e0075084b2082bebb59ea34")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Agv>)))
  "Returns full string definition for message of type '<Agv>"
  (cl:format cl:nil "float64 power~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Agv)))
  "Returns full string definition for message of type 'Agv"
  (cl:format cl:nil "float64 power~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Agv>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Agv>))
  "Converts a ROS message object to a list"
  (cl:list 'Agv
    (cl:cons ':power (power msg))
))
