; Auto-generated. Do not edit!


(cl:in-package pruebas-msg)


;//! \htmlinclude numsteps.msg.html

(cl:defclass <numsteps> (roslisp-msg-protocol:ros-message)
  ((az
    :reader az
    :initarg :az
    :type cl:fixnum
    :initform 0)
   (al
    :reader al
    :initarg :al
    :type cl:fixnum
    :initform 0))
)

(cl:defclass numsteps (<numsteps>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <numsteps>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'numsteps)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name pruebas-msg:<numsteps> is deprecated: use pruebas-msg:numsteps instead.")))

(cl:ensure-generic-function 'az-val :lambda-list '(m))
(cl:defmethod az-val ((m <numsteps>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pruebas-msg:az-val is deprecated.  Use pruebas-msg:az instead.")
  (az m))

(cl:ensure-generic-function 'al-val :lambda-list '(m))
(cl:defmethod al-val ((m <numsteps>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pruebas-msg:al-val is deprecated.  Use pruebas-msg:al instead.")
  (al m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <numsteps>) ostream)
  "Serializes a message object of type '<numsteps>"
  (cl:let* ((signed (cl:slot-value msg 'az)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'al)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <numsteps>) istream)
  "Deserializes a message object of type '<numsteps>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'az) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'al) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<numsteps>)))
  "Returns string type for a message object of type '<numsteps>"
  "pruebas/numsteps")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'numsteps)))
  "Returns string type for a message object of type 'numsteps"
  "pruebas/numsteps")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<numsteps>)))
  "Returns md5sum for a message object of type '<numsteps>"
  "e80bebf4b25dc28d9ae73b0b269a9fdb")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'numsteps)))
  "Returns md5sum for a message object of type 'numsteps"
  "e80bebf4b25dc28d9ae73b0b269a9fdb")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<numsteps>)))
  "Returns full string definition for message of type '<numsteps>"
  (cl:format cl:nil "int16 az~%int16 al~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'numsteps)))
  "Returns full string definition for message of type 'numsteps"
  (cl:format cl:nil "int16 az~%int16 al~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <numsteps>))
  (cl:+ 0
     2
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <numsteps>))
  "Converts a ROS message object to a list"
  (cl:list 'numsteps
    (cl:cons ':az (az msg))
    (cl:cons ':al (al msg))
))
