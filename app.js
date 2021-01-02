const express = require('express');
const mongoose = require('mongoose');
const ejsMate = require('ejs-mate');
const path = require('path');
const { join } = path;
const methodOverride = require('method-override');
const Course = require('./models/course');

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
app.use(methodOverride('_method'));

////////////////////////////////////////
//             ROUTES                 //
////////////////////////////////////////

// GET ROUTES 
app.get('/', (req, res) => {
    res.send('HOME PAGE');
})

app.get('/departments', async (req, res) => {
    const depts = await Course.distinct('department');
    let deptsToCodes = {};

    for (let dept of depts) {
        const data = await Course.findOne({ department: dept })
        deptsToCodes[`${dept}`] = data.code;
    }

    res.render('departments/index', { deptsToCodes, depts });
})

app.get('/departments/:deptCode', async (req, res) => {
    const { deptCode } = req.params;
    const classes = await Course.find({ code: deptCode })
    res.send(classes);
})

app.get('/departments/:deptCode/:courseNum', async (req, res) => {
    const { deptCode, courseNum } = req.params;
    const course = await Course.find({ code: deptCode, number: courseNum });
    res.send(course);
})


app.listen(3000, () => {
    console.log('DARTMOUTH CATALOG SERVER ON PORT 3000');
})

