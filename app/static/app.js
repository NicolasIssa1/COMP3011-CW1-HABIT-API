// API Configuration
const API_BASE = window.location.origin; // Use same server
const DEFAULT_API_KEY = "test-api-key-12345";

// DOM Elements
const apiKeyInput = document.getElementById("apiKey");
const messageEl = document.getElementById("message");
const createHabitForm = document.getElementById("createHabitForm");
const habitsList = document.getElementById("habitsList");
const noHabits = document.getElementById("noHabits");
const habitSelect = document.getElementById("habitSelect");
const analyticsContainer = document.getElementById("analyticsContainer");
const searchInput = document.getElementById("searchHabits");

// State
let allHabits = [];
let filteredHabits = [];

// Utility: Get API Key
function getApiKey() {
    return apiKeyInput.value || DEFAULT_API_KEY;
}

// Utility: Make API Request
async function apiRequest(method, endpoint, body = null) {
    const headers = {
        "X-API-Key": getApiKey(),
        "Content-Type": "application/json"
    };
    
    const options = {
        method,
        headers
    };
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || `Request failed: ${response.status}`);
        }
        
        return data;
    } catch (error) {
        throw error;
    }
}

// Utility: Show Message
function showMessage(text, type = "info") {
    messageEl.textContent = text;
    messageEl.className = `message show ${type}`;
    setTimeout(() => messageEl.classList.remove("show"), 5000);
}

// Load All Habits
async function loadHabits() {
    try {
        displayLoadingState();
        allHabits = await apiRequest("GET", "/habits?limit=100");
        filteredHabits = allHabits;
        renderHabits();
        updateHabitSelect();
    } catch (error) {
        showMessage(`Failed to load habits: ${error.message}`, "error");
    }
}

// Display Loading State
function displayLoadingState() {
    habitsList.innerHTML = `<div style="text-align: center; padding: 20px; color: #999;">
        <div class="loading-spinner" style="margin: 0 auto; vertical-align: middle;"></div> Loading...
    </div>`;
}

// Render Habits List
function renderHabits() {
    habitsList.innerHTML = "";
    
    if (filteredHabits.length === 0) {
        noHabits.classList.remove("hidden");
        return;
    }
    
    noHabits.classList.add("hidden");
    
    filteredHabits.forEach(habit => {
        const habitEl = document.createElement("div");
        habitEl.className = "habit-item";
        habitEl.innerHTML = `
            <div class="habit-info">
                <h3>${escapeHtml(habit.name)}</h3>
                <div class="habit-meta">
                    ${habit.description ? `<p>${escapeHtml(habit.description)}</p>` : ""}
                    <p>Frequency: <strong>${habit.frequency}</strong> | 
                       Status: <strong>${habit.is_active ? "Active" : "Inactive"}</strong></p>
                </div>
            </div>
            <div class="habit-actions">
                <button class="btn-success btn-small" onclick="markHabitDone(${habit.id})">
                    ✓ Mark Done Today
                </button>
                <button class="btn-secondary btn-small" onclick="viewHabitStats(${habit.id})">
                    📊 Stats
                </button>
                <button class="btn-danger btn-small" onclick="deleteHabit(${habit.id})">
                    🗑️ Delete
                </button>
            </div>
        `;
        habitsList.appendChild(habitEl);
    });
}

// Create Habit
createHabitForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const name = document.getElementById("habitName").value.trim();
    const description = document.getElementById("habitDescription").value.trim();
    const frequency = document.getElementById("habitFrequency").value;
    
    if (!name) {
        showMessage("Habit name is required", "error");
        return;
    }
    
    try {
        const newHabit = await apiRequest("POST", "/habits", {
            name,
            description,
            frequency
        });
        
        showMessage(`Habit "${newHabit.name}" created! 🎉`, "success");
        createHabitForm.reset();
        await loadHabits();
    } catch (error) {
        showMessage(`Failed to create habit: ${error.message}`, "error");
    }
});

// Mark Habit as Done
async function markHabitDone(habitId) {
    const today = new Date().toISOString().split("T")[0];
    
    try {
        await apiRequest("POST", `/habits/${habitId}/logs`, {
            date: today,
            notes: ""
        });
        
        showMessage("Habit marked as done! 🎉", "success");
        await loadHabits();
    } catch (error) {
        if (error.message.includes("409")) {
            showMessage("Already logged for today!", "info");
        } else {
            showMessage(`Failed to mark habit: ${error.message}`, "error");
        }
    }
}

// Delete Habit
async function deleteHabit(habitId) {
    if (!confirm("Are you sure you want to delete this habit?")) return;
    
    try {
        await apiRequest("DELETE", `/habits/${habitId}`);
        showMessage("Habit deleted", "success");
        await loadHabits();
    } catch (error) {
        showMessage(`Failed to delete habit: ${error.message}`, "error");
    }
}

// View Habit Stats (Streak)
async function viewHabitStats(habitId) {
    try {
        const habit = allHabits.find(h => h.id === habitId);
        habitSelect.value = habitId;
        await loadAnalytics();
    } catch (error) {
        showMessage(`Failed to load stats: ${error.message}`, "error");
    }
}

// Load Analytics for Selected Habit
async function loadAnalytics() {
    const habitId = habitSelect.value;
    analyticsContainer.innerHTML = "";
    
    if (!habitId) return;
    
    try {
        const streak = await apiRequest("GET", `/habits/${habitId}/streak`);
        
        const html = `
            <div class="analytics-item">
                <h4>Current Streak</h4>
                <div class="value">${streak.current_streak} days</div>
            </div>
            <div class="analytics-item">
                <h4>Longest Streak</h4>
                <div class="value">${streak.longest_streak} days</div>
            </div>
            <div class="analytics-item">
                <h4>Total Completions</h4>
                <div class="value">${streak.total_completions}</div>
            </div>
        `;
        
        analyticsContainer.innerHTML = html;
    } catch (error) {
        analyticsContainer.innerHTML = `<div class="alert alert-warning">Failed to load analytics: ${error.message}</div>`;
    }
}

// Update Habit Select Dropdown
function updateHabitSelect() {
    const currentValue = habitSelect.value;
    habitSelect.innerHTML = '<option value="">-- Choose a habit --</option>';
    
    allHabits.forEach(habit => {
        const option = document.createElement("option");
        option.value = habit.id;
        option.textContent = habit.name;
        habitSelect.appendChild(option);
    });
    
    habitSelect.value = currentValue;
}

// Search Habits
searchInput.addEventListener("input", (e) => {
    const query = e.target.value.toLowerCase();
    filteredHabits = allHabits.filter(habit =>
        habit.name.toLowerCase().includes(query) ||
        habit.description.toLowerCase().includes(query)
    );
    renderHabits();
});

// Analytics Change Handler
habitSelect.addEventListener("change", loadAnalytics);

// Utility: Escape HTML
function escapeHtml(text) {
    const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Initialize
loadHabits();
