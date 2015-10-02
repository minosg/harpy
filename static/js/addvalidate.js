// Form validation
function validate()
{
   if( document.addForm.color.value == "" )
   {
      if (document.addForm.remove.checked) {
          return true;
      } else {
          alert( "Please Select a Color" );
          return false;
      }


   }
   if( document.addForm.macdata.value == "" )
   {
      alert( "Please Select a Mac Address from the list" );
      return false;
   }
   return true;
}
