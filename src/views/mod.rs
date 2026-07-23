//! The views module contains the components for all Layouts and Routes for our app. Each layout and route in our [`Route`]
//! enum will render one of these components.
//!
//! The [`Navbar`] component will be rendered on all pages of our app since every page is under the layout. The layout defines
//! a common wrapper around all child routes.

mod home;
pub use home::Home;

mod dialogue;
pub use dialogue::{Dialogue, DialoguePost};

mod matter;
pub use matter::Matter;

mod random;
pub use random::Random;

mod navbar;
pub use navbar::Navbar;
