var f=new Vue({
    el: '#vf',
    data:{
        fname:document.getElementById('inputFname').value,
        pass:'',
        lname:document.getElementById('inputLname').value,
        ferr:0,
        perr:0,
        lerr:0
    },
    watch: {
        fname: function(){
            if(this.fname.length<3)
            {
                this.ferr=1;
            }
            else{
                this.ferr=0;
            }
        },
        lname: function(){   
            if(this.lname.length<2)
            {
                this.lerr=1;
            }
            else{
                this.lerr=0;
            }
        },
        pass: function(){
            if(this.pass.length<6)
            {
                this.perr=1;
            }
            else{
                this.perr=0;
            }
        }
    }
    
})