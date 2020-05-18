update_dict(), is to update the dictionary when given the path and the variable to be updated with

append_dict(), when given the path and the variable,
            appends the to the list at the end of the path(end of path being the key of the list)
            NOTE
            the end of the path must be a list for the appending to work!!

remove_item(), removes the value of the last item in the path regardless of it being a key or a value
               eg."test.alpha.start.1"---- removes the index 1 item of the list at then end 
                  "test.alpha.start" ----- removes the value of key "start"

.changes = shows the changes before restarting in a form of a list such that it is in order

.og_dict = shows the original dictionary inputted


__restart__() has to be used after every function such that the function such that its resetted back to the original dict 

if you you don't restart you would work with the result of the function if you continue 


default path delimiter would be '.'
but it can be altered to be '_' or any other symbols 
eg. by adding the parameter delimeter = '_'



