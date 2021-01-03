const express = require('express');
const mongoose = require('mongoose');
const ejsMate = require('ejs-mate');
const path = require('path');
const { join } = path;
const methodOverride = require('method-override');
const Course = require('./models/course');
const Review = require('./models/review');
const { reverse } = require('dns');

// Connects Mongoose to local DB
mongoose.connect('mongodb://localhost:27017/dartmouthcatalog', {
    useNewUrlParser: true,
    useCreateIndex: true,
    useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on("error", console.error.bind(console, "Connection error:"));
db.once("open", () => {
    console.log("Database connected");
})

const app = express();

app.engine('ejs', ejsMate);
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.urlencoded({ extended: true }));
app.use(express.json()) // helps parse JSON in the body of a POST request and make req.body substantive 

app.use(methodOverride('_method'));

////////////////////////////////////////
//             ROUTES                 //
////////////////////////////////////////

app.get('/', (req, res) => {
    res.send('HOME PAGE');
})

app.get('/departments', async (req, res) => {
    const codes = await Course.distinct('code');
    let codesToDepts = {};

    for (let code of codes) {
        const data = await Course.findOne({ code: code })
        codesToDepts[`${code}`] = data.department;
    }

    res.render('departments/index', { codesToDepts, codes });
})

app.get('/departments/:deptCode', async (req, res) => {
    const { deptCode } = req.params;
    const courses = await Course.find({ code: deptCode });
    let deptName = await Course.findOne({ code: deptCode });
    deptName = deptName.department;
    res.render('courses/index', { deptCode, courses, deptName });
})

app.get('/departments/:deptCode/:courseNum', async (req, res) => {
    const { deptCode, courseNum } = req.params;
    const course = await Course.findOne({ code: deptCode, number: courseNum }).populate('reviews');
    const similarCourses = await Course.aggregate([{ $match: { code: deptCode } }, { $sample: { size: 7 } }]);
    res.render('courses/show', { course, similarCourses });
})

app.get('/courses', async (req, res) => {
    const courses = await Course.find();
    const deptName = "All"
    res.render('courses/index', { courses, deptName });
})

app.get('/lucky', async (req, res) => {
    const course = await Course.aggregate([{ $sample: { size: 1 } }]);
    res.redirect(`/departments/${course[0].code}/${course[0].number}`);
})

app.post('/departments/:deptCode/:courseNum/reviews', async (req, res) => {
    const { deptCode, courseNum } = req.params;
    const course = await Course.findOne({ code: deptCode, number: courseNum });
    const review = new Review(req.body); 
    course.reviews.push(review); 
    await review.save(); 
    await course.save(); 
    res.redirect(`/departments/${deptCode}/${courseNum}`); 
})

// @TODO: determine whether to support review deletion functionality
app.delete('/departments/:deptCode/:courseNum/reviews/:reviewID', async (req, res) => {
    const { deptCode, courseNum, reviewID } = req.params; 
    await Review.findByIdAndDelete(reviewID); 
    await Course.updateOne({ reviews: { $in: [reviewID] } }, { $pull: { reviews: { $in: [reviewID] } } })
    res.redirect(`/departments/${deptCode}/${courseNum}`); 
})

app.all('*', (req, res, next) => {
    res.status(400).send("Couldn't find what you were looking for!");
})

app.listen(3000, () => {
    console.log('DARTMOUTH CATALOG SERVER ON PORT 3000');
})

