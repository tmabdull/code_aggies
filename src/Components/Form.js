import React, { useState } from 'react';

function TextBox() {
    const [mealPreference, setMealPreference] = useState('');

    const handleMealPreferenceChange = (event) => {
        setMealPreference(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        const location = event.target.location.value;
        const data = { location, mealPreference };
        console.log(data);
        fetch('http://localhost:8001', {
            method: 'POST',
            mode: 'no-cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch((error) => {
            console.error('Error:', error);
        });
    };

    return (
        <div>
            <h2>Please input your preferences</h2>
            <form onSubmit={handleSubmit}>
                <div>
                <label>
                    Your Location:     
                    <input type="text" name="location" />
                </label>
                </div>
                <br />
                <div>
                <label>
                    Meal Preferences:
                    <select value={mealPreference} onChange={handleMealPreferenceChange} name="mealPreferences">
                        <option value="">Select an option</option>
                        <option value="Halal">Halal</option>
                        <option value="Vegan">Vegan</option>
                        <option value="Vegetarian">Vegetarian</option>
                        <option value="Anything">Anything</option>
                    </select>
                </label>
                </div>
                <br />
                <input type="submit" value="Submit" />
            </form>
        </div>
    );
}

export default TextBox;
