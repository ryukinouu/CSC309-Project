// SeekerAppList.js
import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

import Header from '../../../components/Header/Header.jsx';
import Footer from '../../../components/Footer/Footer.jsx';
import '../../../styles/search.css'
import '../../../styles/base.css'

import 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js'
import 'https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js'


const SeekerAppList = () => {
  const [jsonCardData, setCardData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [sortOption, setSortOption] = useState('name');
  const location = useLocation();

  const cardData = [
    { id: 1, name: 'Alice', description: 'Meet Alice, who is a cute kitty!' },
    { id: 1, name: 'Alice', description: 'Meet Alice, who is a cute kitty!' },
    { id: 1, name: 'Alice', description: 'Meet Alice, who is a cute kitty!' },
    // Add more card data as needed
  ];

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const statusFilter = searchParams.get('filter');
    const sortFilter = searchParams.get('sort');

    fetch(`http://127.0.0.1:8000/applications/?page=${currentPage}&status=${statusFilter || ''}&sort=${sortFilter || ''}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
      })
      .then((response) => response.json())
      .then((data) => {
        setCardData(data.applications);
        setTotalPages(data.total_pages);
      })
      .catch((error) => console.error('Error fetching applications:', error));
  }, [currentPage, location.search, sortOption]);

  const handlePageChange = direction => {
    setCurrentPage(prevPage =>
        direction === 'next' ? Math.min(prevPage + 1, totalPages) : Math.max(prevPage - 1, 1)
    );
  };

  const handleSortChange = (option) => {
    setSortOption(option);
  };
  
  return (
    <div>
      <div class="page_container">
        <div class="content_wrap">
          <Header />
          <main>
            <div class="search-wrapper">
              <h1 class="display-6 lead text-center mt-5">My Applications</h1>
              <div class="input-group mt-5 px-5">
                <input type="search" class="form-control rounded" placeholder="Search for keywords" aria-label="Search" aria-describedby="search-addon" />
                <div class="btn-group">
                  <button class="btn btn-primary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Search By
                  </button>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#">Search All</a></li>
                    <li><a class="dropdown-item" href="#">Age</a></li>
                    <li><a class="dropdown-item" href="#">Breed</a></li>
                    <li><a class="dropdown-item" href="#">Colour</a></li>
                    <li><a class="dropdown-item" href="#">Gender</a></li>
                    <li><a class="dropdown-item" href="#">Location</a></li>
                    <li><a class="dropdown-item" href="#">Size</a></li>
                  </ul>
                </div>
                <button type="button" class="btn btn-outline-primary p-3">Search</button>
              </div>

              <div class="sort-wrapper text-end">
                <div class=" sort-text"> Sort by
                  <div class="btn-group sort-btn-wrapper">
                    <button class="btn btn-primary dropdown-toggle sort-btn" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                      Name (A-Z)
                    </button>
                    <ul class="dropdown-menu">
                      <li><a class="dropdown-item" onClick={() => handleSortChange('name')}>Name (A-Z)</a></li>
                      <li><a class="dropdown-item" onClick={() => handleSortChange('age')}>Age (Old-Young)</a></li>
                      <li><a class="dropdown-item" onClick={() => handleSortChange('date')}>Date (Recent-Old)</a></li>
                    </ul>
                  </div>
                </div>
                <div className="card-container row row-cols-1 row-cols-md-3 g-4">
                  {/* Map through cardData to create cards */}
                  {cardData.map((card) => (
                    <div key={card.id} className="col">
                      <div className="card">
                        <div className="card-body">
                          <h5 className="card-title">{card.name}</h5>
                          <p className="card-text">{card.description}</p>
                        </div>
                        <div className="card-footer">
                          <button type="button" class="btn btn-success">
                              Details
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="pagination-container">
                  <button type="button" class="btn btn-primary"
                      onClick={() => handlePageChange('previous')} 
                      disabled={currentPage === 1}>
                      Previous
                  </button>
                  <span>{`Page: ${currentPage} of ${totalPages}`}</span>
                  <button type="button" class="btn btn-primary"
                      onClick={() => handlePageChange('next')}
                      disabled={currentPage === totalPages}>
                      Next
                  </button>
              </div>
              </div>
            </div>
          </main>
          <Footer />
        </div>
      </div>
    </div>
  );
};

export default SeekerAppList;