import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png"

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [dealersListFull, setDealersListFull] = useState([]);  // keep full list for filtering
  const [states, setStates] = useState([]);

  let dealer_url = "/djangoapp/get_dealers";

  // Filter dealers locally by state
  const filterDealers = (state) => {
    if (state === "All" || state === "") {
      setDealersList(dealersListFull);  // reset filter
      return;
    }
    const filtered = dealersListFull.filter(dealer => dealer.state === state);
    setDealersList(filtered);
  }

  const get_dealers = async () => {
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();
    // No status code in backend response, so no if check here
    let all_dealers = retobj.dealerships || [];
    let statesSet = new Set();
    all_dealers.forEach((dealer) => {
      statesSet.add(dealer.state);
    });

    setStates(Array.from(statesSet));
    setDealersList(all_dealers);
    setDealersListFull(all_dealers);
  }

  useEffect(() => {
    get_dealers();
  }, []);
  

  let isLoggedIn = sessionStorage.getItem("username") != null ? true : false;

  return (
    <div>
      <Header />
      <table className='table'>
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select name="state" id="state" onChange={(e) => filterDealers(e.target.value)}>
                <option value="" disabled hidden>State</option>
                <option value="All">All States</option>
                {states.map(state => (
                  <option key={state} value={state}>{state}</option>
                ))}
              </select>
            </th>
            {isLoggedIn && <th>Review Dealer</th>}
          </tr>
        </thead>
        <tbody>
          {dealersList.map(dealer => (
            <tr key={dealer.id}>
              <td>{dealer.id}</td>
              <td><a href={'/dealer/' + dealer['id']}>{dealer['name']}</a></td>
              <td>{dealer.city}</td>
              <td>{dealer.address}</td>
              <td>{dealer.zip}</td>
              <td>{dealer.state}</td>
              {isLoggedIn && (
                <td><a href={`/postreview/${dealer.id}`}><img src={review_icon} className="review_icon" alt="Post Review" /></a></td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Dealers;
