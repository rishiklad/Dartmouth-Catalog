const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const Course = require('./course'); 

const ReviewSchema = new Schema({
    author: String,
    term: String,
    professor: String,
    rating: Number,
    body: String
})

module.exports = mongoose.model("Review", ReviewSchema); 
