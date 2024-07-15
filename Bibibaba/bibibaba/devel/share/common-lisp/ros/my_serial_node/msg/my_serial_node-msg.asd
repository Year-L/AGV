
(cl:in-package :asdf)

(defsystem "my_serial_node-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Agv" :depends-on ("_package_Agv"))
    (:file "_package_Agv" :depends-on ("_package"))
    (:file "Balance" :depends-on ("_package_Balance"))
    (:file "_package_Balance" :depends-on ("_package"))
  ))