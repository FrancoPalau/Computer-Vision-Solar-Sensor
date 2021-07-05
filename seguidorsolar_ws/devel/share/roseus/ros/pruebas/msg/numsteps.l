;; Auto-generated. Do not edit!


(when (boundp 'pruebas::numsteps)
  (if (not (find-package "PRUEBAS"))
    (make-package "PRUEBAS"))
  (shadow 'numsteps (find-package "PRUEBAS")))
(unless (find-package "PRUEBAS::NUMSTEPS")
  (make-package "PRUEBAS::NUMSTEPS"))

(in-package "ROS")
;;//! \htmlinclude numsteps.msg.html


(defclass pruebas::numsteps
  :super ros::object
  :slots (_az _al ))

(defmethod pruebas::numsteps
  (:init
   (&key
    ((:az __az) 0)
    ((:al __al) 0)
    )
   (send-super :init)
   (setq _az (round __az))
   (setq _al (round __al))
   self)
  (:az
   (&optional __az)
   (if __az (setq _az __az)) _az)
  (:al
   (&optional __al)
   (if __al (setq _al __al)) _al)
  (:serialization-length
   ()
   (+
    ;; int16 _az
    2
    ;; int16 _al
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int16 _az
       (write-word _az s)
     ;; int16 _al
       (write-word _al s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int16 _az
     (setq _az (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _al
     (setq _al (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get pruebas::numsteps :md5sum-) "e80bebf4b25dc28d9ae73b0b269a9fdb")
(setf (get pruebas::numsteps :datatype-) "pruebas/numsteps")
(setf (get pruebas::numsteps :definition-)
      "int16 az
int16 al
")



(provide :pruebas/numsteps "e80bebf4b25dc28d9ae73b0b269a9fdb")


