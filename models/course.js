const mongoose = require('mongoose'); 
const Schema = mongoose.Schema; 
const Review = require('./review'); 

const CourseSchema = new Schema({
    department: String, 
    code: String, 
    number: Number, 
    title: String, 
    description: String, 
    url: String, 
    reviews: [
        {
            type: Schema.Types.ObjectId, 
            ref: "Review"
        }
    ]
})

// QUERY MIDDLEWARE THAT PASSES IN THE COURSE IT JUST DELETED
// THIS MIDDLEWARE ENSURES THAT AFTER WE DELETE A COURSE, ALL ASSOCIATED REVIEWS GO AWAY 
CourseSchema.post('findOneAndDelete', async function (doc) {
    if(doc) {
        await Review.deleteMany({
            _id: {
                $in: doc.reviews
            }
        })
    }
})

module.exports = mongoose.model('Course', CourseSchema); 