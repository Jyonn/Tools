from App.Doris.library_booking import LibraryBooking
from Base.router import Router

dorisRouter = Router()

dorisRouter.register('library-booking', LibraryBooking)
