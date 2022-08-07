var mysql = require('mysql');
var connection = mysql.createConnection(
    {
        host: '34.80.39.159',
        user:'chench',
        database:'Fiteat'
    }
);

function createUser(account,password){
    connection.connect();
    var sql = "INSERT INTO User (account,password) VALUES ('" + account + "', '"+ password + "');";
    connection.query(sql,function(err,result){
        if(err){
            console.log(err);
            return;
        }
        console.log('creat user successfully');
    });
    connection.end();
}

function listUser(){
    connection.connect();
    var sql = 'SELECT * FROM User';
    connection.query(sql,function (err , result) { 
        if ( err ) { 
            console . log (err) ;
            return ;
        }
        console.log(result);
    });
    connection.end();
}
function updateUser(account,height,weight,workload,BMI,TDEE){
    connection.connect();
    var sql = "UPDATE User SET height=" + height +
    ",weight=" + weight+",workload='"+ workload +"',BMI="+ BMI + ",TDEE="+ TDEE + 
    " WHERE account='" + account + "';";
    connection.query(sql,function(err,result){
        if(err){
            console.log(err);
            return;
        }
        console.log('update user successfully');
    });
    connection.end();
}
function deleteUser(account){
    connection.connect();
    var sql = "DELETE FROM User WHERE account='" + account + "';";
    connection.query(sql,function(err,result){
        if(err){
            console.log(err);
            return;
        }
        console.log('delete user successfully');
    });
    connection.end();
}

// createUser('team6worker','test000');
// listUser();
// updateUser('chench',173,65,'mid',21.7,1622);
// deleteUser('team6worker')