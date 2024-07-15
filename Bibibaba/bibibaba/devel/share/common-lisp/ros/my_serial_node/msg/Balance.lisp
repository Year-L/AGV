; Auto-generated. Do not edit!


(cl:in-package my_serial_node-msg)


;//! \htmlinclude Balance.msg.html

(cl:defclass <Balance> (roslisp-msg-protocol:ros-message)
  ((weight
    :reader weight
    :initarg :weight
    :type cl:float
    :initform 0.0))
)

(cl:defclass Balance (<Balance>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Balance>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Balance)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name my_serial_node-msg:<Balance> is deprecated: use my_serial_node-msg:Balance instead.")))

(cl:ensure-generic-function 'weight-val :lambda-list '(m))
(cl:defmethod weight-val ((m <Balance>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader my_serial_node-msg:weight-val is deprecated.  Use my_serial_node-msg:weight instead.")
  (weight m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Balance>) ostream)
  "Serializes a message object of type '<Balance>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'weight))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Balance>) istream)
  "Deserializes a message object of type '<Balance>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'weight) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Balance>)))
  "Returns string type for a message object of type '<Balance>"
  "my_serial_node/Balance")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Balance)))
  "Returns string type for a message object of type 'Balance"
  "my_serial_node/Balance")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Balance>)))
  "Returns md5sum for a message object of type '<Balance>"
  "41998f6691705e7d3db1ca4195275ab0")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Balance)))
  "Returns md5sum for a message object of type 'Balance"
  "41998f6691705e7d3db1ca4195275ab0")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Balance>)))
  "Returns full string definition for message of type '<Balance>"
  (cl:format cl:nil "float64 weight~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Balance)))
  "Returns full string definition for message of type 'Balance"
  (cl:format cl:nil "float64 weight~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Balance>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Balance>))
  "Converts a ROS message object to a list"
  (cl:list 'Balance
    (cl:cons ':weight (weight msg))
))
