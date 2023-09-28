from Cogs.Class.ticket import Ticket

def return_class(class_name):
    match class_name:
        case "Ticket":
            return "from Cogs.Class.ticket import Ticket"
        
