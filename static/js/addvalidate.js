// Form validation
function validate()
{
   if( document.addForm.color.value == "" )
   {
      alert( "Please Select a Color" );
      return false;
   }
   if( document.addForm.macdata.value == "" )
   {
      alert( "Please Select a Mac Address from the list" );
      return false;
   }
   return true;
}
