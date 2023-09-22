
var myName = "Thinh";

let sa = " sa" //let is used locally
const pi = 21 // const can't changed

console.log(sa.length)


var s = 21

s *= 4

var tr = "I am \"Thinh\""

function reverseString(s){
    
    newString = ""
    for (let i = s.length-1; i > -1; i-= 1){
        newString += s[i];
    }

    return newString
}
const testsa = reverseString("Hello World")

console.log(testsa)
