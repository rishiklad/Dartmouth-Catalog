const mongoose = require('mongoose'); 
const Schema = mongoose.Schema; 

const CourseSchema = new Schema({
    department: String, 
    code: String, 
    number: Number, 
    title: String, 
    description: String, 
    url: String
})

module.exports = mongoose.model('Course', CourseSchema); 