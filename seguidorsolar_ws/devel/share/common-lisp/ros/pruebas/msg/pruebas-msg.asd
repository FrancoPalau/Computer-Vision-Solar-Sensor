
(cl:in-package :asdf)

(defsystem "pruebas-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "numsteps" :depends-on ("_package_numsteps"))
    (:file "_package_numsteps" :depends-on ("_package"))
  ))