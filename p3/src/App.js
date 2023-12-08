import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import Notifications from './pages/Notifications';
import Error from './pages/Error';

import Login from './pages/Accounts/Login';
import Signup from './pages/Accounts/Signup';
import Profile from './pages/Accounts/Profile';
import Shelters from './pages/Accounts/Shelters';
import Shelter from './pages/Accounts/Shelter';

import Search from './pages/Search';
import NewPet from './pages/NewPet';
import EditPet from './pages/EditPet';
import PetDetails from './pages/PetDetails'

import AppList from './pages/Application/List';
import AppDetail from './pages/Application/Detail';
import AppApply from './pages/Application/Create';

import BlogCreate from './pages/Blog/BlogCreate';
import BlogRetrieve from './pages/Blog/BlogRetrieve';
import BlogEdit from './pages/Blog/BlogEdit';
import BlogList from './pages/Blog/BlogList';

import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/home" element={<Home />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/applications" element={<AppList />} />
        <Route path="/listings" element={<Search />} />
        <Route path="/listings/:id" element={<PetDetails />} />
        <Route path="/newpet" element={<NewPet />} />
        <Route path="/editpet/:pk" element={<EditPet />} />
        <Route path="*" element={<Error />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/profile/:username" element={<Profile />} />
        <Route path="/shelters/" element={<Shelters />} />
        <Route path="/shelters/:username" element={<Shelter />} />
        <Route path="/applications/*" element={<ApplicationRoutes />} />
        <Route path="/blogs/:username/create" element={<BlogCreate />} />
        <Route path="/blogs/:username/:pk/edit" element={<BlogEdit />} />
        <Route path="/blogs/:username/:pk" element={<BlogRetrieve />} />
      </Routes>
    </Router>
  );
};

const ApplicationRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<AppList />} />
      <Route path="details/:appID" element={<AppDetail />} />
      <Route path="create/:petID" element={<AppApply />} />
    </Routes>
  );
};


export default App;

