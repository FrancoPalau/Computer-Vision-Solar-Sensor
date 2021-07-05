// Auto-generated. Do not edit!

// (in-package pruebas.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class numsteps {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.az = null;
      this.al = null;
    }
    else {
      if (initObj.hasOwnProperty('az')) {
        this.az = initObj.az
      }
      else {
        this.az = 0;
      }
      if (initObj.hasOwnProperty('al')) {
        this.al = initObj.al
      }
      else {
        this.al = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type numsteps
    // Serialize message field [az]
    bufferOffset = _serializer.int16(obj.az, buffer, bufferOffset);
    // Serialize message field [al]
    bufferOffset = _serializer.int16(obj.al, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type numsteps
    let len;
    let data = new numsteps(null);
    // Deserialize message field [az]
    data.az = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [al]
    data.al = _deserializer.int16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'pruebas/numsteps';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e80bebf4b25dc28d9ae73b0b269a9fdb';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int16 az
    int16 al
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new numsteps(null);
    if (msg.az !== undefined) {
      resolved.az = msg.az;
    }
    else {
      resolved.az = 0
    }

    if (msg.al !== undefined) {
      resolved.al = msg.al;
    }
    else {
      resolved.al = 0
    }

    return resolved;
    }
};

module.exports = numsteps;
