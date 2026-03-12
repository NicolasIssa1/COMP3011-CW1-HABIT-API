// ====================================================================
// HABIT TRACKER - VANILLA JS (WORKING VERSION)
// ====================================================================

const API_BASE = "/api";
const DEFAULT_API_KEY = "test-api-key-12345";
const STORAGE_KEY_API = "habit_api_key";

// State Management
const appState = {
    habits: [],
    filteredHabits: [],
    selectedHabitId: null,
    isLoading: false,
};

// ====================================================================
// API KEY MANAGEMENT
// ====================================================================

function getStoredApiKey() {
    return localStorage.getItem(STORAGE_KEY_API) || DEFAULT_API_KEY;
}

function saveApiKey(key) {
    localStorage.setItem(STORAGE_KEY_API, key);
}

// ====================================================================
// API REQUESTS
// ====================================================================

async function apiRequest(method, endpoint, body = null) {
    const headers = {
        "X-API-Key": getStoredApiKey(),
        "Content-Type": "application/json"
    };

    const options = { method, headers };
    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        
        // Handle responses with no body (204 No Content, 304 Not Modified)
        let data = {};
        if (response.status !== 204 && response.status !== 304) {
            try {
                data = await response.json();
            } catch (e) {
                // If JSON parsing fails, continue with empty object
                console.warn("Failed to parse response JSON:", e);
                data = {};
            }
        }

        // Check response status and throw error if not ok
        if (!response.ok) {
            const errorMessage = data.detail || `Request failed with status ${response.status}`;
            const err = new Error(errorMessage);
            err.status = response.status;
            throw err;
        }

        return data;
    } catch (error) {
        throw error;
    }
}

// ====================================================================
// TOAST NOTIFICATIONS
// ====================================================================

class ToastManager {
    constructor() {
        this.container = document.getElementById("toastContainer");
    }

    show(message, type = "info", duration = 4000) {
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span>${escapeHtml(message)}</span>
            <button class="toast-close" aria-label="Close">&times;</button>
        `;

        this.container.appendChild(toast);
        const closeBtn = toast.querySelector(".toast-close");
        closeBtn.addEventListener("click", () => this.remove(toast));

        if (duration > 0) {
            setTimeout(() => this.remove(toast), duration);
        }

        return toast;
    }

    success(message, duration = 3000) {
        this.show(message, "success", duration);
    }

    error(message, duration = 5000) {
        this.show(message, "error", duration);
    }

    info(message, duration = 3000) {
        this.show(message, "info", duration);
    }

    warning(message, duration = 4000) {
        this.show(message, "warning", duration);
    }

    remove(toast) {
        toast.classList.add("removing");
        setTimeout(() => toast.remove(), 300);
    }
}

const toast = new ToastManager();

// ====================================================================
// MODAL MANAGER
// ====================================================================

class ModalManager {
    static open(modalElement) {
        modalElement.classList.add("show");
    }

    static close(modalElement) {
        modalElement.classList.remove("show");
    }

    static isOpen(modalElement) {
        return modalElement.classList.contains("show");
    }

    static closeAll() {
        document.querySelectorAll(".modal.show").forEach(modal => {
            this.close(modal);
        });
    }
}

// ====================================================================
// CONFIRM DIALOG
// ====================================================================

function showConfirmDialog(title, message) {
    return new Promise((resolve) => {
        const confirmDialog = document.getElementById("confirmDialog");
        const confirmTitle = document.getElementById("confirmTitle");
        const confirmMessage = document.getElementById("confirmMessage");
        const confirmOk = document.getElementById("confirmOk");
        const confirmCancel = document.getElementById("confirmCancel");

        confirmTitle.textContent = title;
        confirmMessage.textContent = message;

        const handleOk = () => {
            cleanup();
            resolve(true);
        };

        const handleCancel = () => {
            cleanup();
            resolve(false);
        };

        const cleanup = () => {
            confirmOk.removeEventListener("click", handleOk);
            confirmCancel.removeEventListener("click", handleCancel);
            ModalManager.close(confirmDialog);
        };

        confirmOk.addEventListener("click", handleOk);
        confirmCancel.addEventListener("click", handleCancel);

        ModalManager.open(confirmDialog);
    });
}

// ====================================================================
// API KEY MODAL
// ====================================================================

function initApiKeyModal() {
    // Use correct IDs from the actual HTML
    const apiKeyBtn = document.getElementById("apiKeyToggle");
    const apiKeyModal = document.getElementById("apiKeyModal");
    const apiKeyInput = document.getElementById("apiKeyInput");
    const saveApiKeyBtn = document.getElementById("saveApiKey");
    const cancelApiKeyBtn = document.getElementById("cancelApiKey");
    const modalClose = document.querySelector("#apiKeyModal .modal-close");

    // Check if all required elements exist
    if (!apiKeyBtn || !apiKeyModal || !apiKeyInput || !saveApiKeyBtn || !cancelApiKeyBtn) {
        console.warn("API key modal elements not found; skipping API key modal init.");
        return;
    }

    apiKeyBtn.addEventListener("click", () => {
        apiKeyInput.value = getStoredApiKey();
        ModalManager.open(apiKeyModal);
    });

    saveApiKeyBtn.addEventListener("click", () => {
        const newKey = apiKeyInput.value.trim();
        if (!newKey) {
            toast.error("API key cannot be empty");
            return;
        }
        saveApiKey(newKey);
        ModalManager.close(apiKeyModal);
        toast.success("API key saved!");
    });

    cancelApiKeyBtn.addEventListener("click", () => {
        ModalManager.close(apiKeyModal);
    });

    // Close modal when clicking the close button (if it exists)
    if (modalClose) {
        modalClose.addEventListener("click", () => {
            ModalManager.close(apiKeyModal);
        });
    }

    // Close modal on Enter key in input
    apiKeyInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            saveApiKeyBtn.click();
        }
    });
}

// ====================================================================
// HABIT MANAGEMENT
// ====================================================================

async function loadHabits() {
    try {
        appState.isLoading = true;
        appState.habits = await apiRequest("GET", "/habits?limit=100");
        appState.filteredHabits = appState.habits;
        renderHabits();
        updateHabitSelect();
    } catch (error) {
        toast.error(`Failed to load habits: ${error.message}`);
    } finally {
        appState.isLoading = false;
    }
}

function renderHabits() {
    const habitsList = document.getElementById("habitsList");
    const noHabits = document.getElementById("noHabits");

    habitsList.innerHTML = "";

    if (appState.filteredHabits.length === 0) {
        noHabits.classList.remove("hidden");
        return;
    }

    noHabits.classList.add("hidden");

    appState.filteredHabits.forEach((habit) => {
        const card = createHabitCard(habit);
        habitsList.appendChild(card);
    });
}

function createHabitCard(habit) {
    const card = document.createElement("div");
    card.className = "habit-card";
    card.innerHTML = `
        <div class="habit-card-header">
            <h3>${escapeHtml(habit.name)}</h3>
            <span class="habit-badge">${habit.frequency}</span>
        </div>
        ${
            habit.description
                ? `<p class="habit-description">${escapeHtml(habit.description)}</p>`
                : ""
        }
        <div class="habit-meta">
            <span>📊 ID: ${habit.id}</span>
            <span>${habit.is_active ? "✓ Active" : "✗ Inactive"}</span>
        </div>
        <div class="habit-actions">
            <button class="btn btn-primary btn-sm" data-action="view" data-id="${habit.id}">
                📋 View
            </button>
            <button class="btn btn-success btn-sm" data-action="mark-done" data-id="${habit.id}">
                ✓ Done Today
            </button>
            <button class="btn btn-danger btn-sm" data-action="delete" data-id="${habit.id}">
                🗑️ Delete
            </button>
        </div>
    `;

    // Event delegation
    const viewBtn = card.querySelector('[data-action="view"]');
    const markDoneBtn = card.querySelector('[data-action="mark-done"]');
    const deleteBtn = card.querySelector('[data-action="delete"]');

    viewBtn.addEventListener("click", () => showHabitDetails(habit.id));
    markDoneBtn.addEventListener("click", () => markHabitDone(habit.id, markDoneBtn));
    deleteBtn.addEventListener("click", () => deleteHabit(habit.id));

    return card;
}

// ====================================================================
// HABIT DETAILS
// ====================================================================

async function showHabitDetails(habitId) {
    try {
        appState.selectedHabitId = habitId;
        const habit = appState.habits.find((h) => h.id === habitId);

        if (!habit) {
            toast.error("Habit not found");
            return;
        }

        const detailsSection = document.getElementById("detailsSection");
        const detailsTitle = document.getElementById("detailsTitle");
        const streakStats = document.getElementById("streakStats");

        detailsTitle.textContent = habit.name;

        // Load streak stats
        const streak = await apiRequest("GET", `/habits/${habitId}/streak`);
        streakStats.innerHTML = `
            <div class="stat-card">
                <div class="stat-label">Current Streak</div>
                <div class="stat-value">${streak.current_streak}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Longest Streak</div>
                <div class="stat-value">${streak.longest_streak}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Completions</div>
                <div class="stat-value">${streak.total_completions}</div>
            </div>
        `;

        // Load logs
        await loadHabitLogs(habitId);

        // Show details section
        detailsSection.classList.remove("hidden");

        // Update button handlers
        document.getElementById("markDoneTodayBtn").onclick = () => markHabitDone(habitId);
        document.getElementById("deleteHabitBtn").onclick = () => deleteHabit(habitId);
        document.getElementById("closeDetails").onclick = () => {
            detailsSection.classList.add("hidden");
            appState.selectedHabitId = null;
        };
    } catch (error) {
        toast.error(`Failed to load habit details: ${error.message}`);
    }
}

async function loadHabitLogs(habitId) {
    try {
        const logs = await apiRequest("GET", `/habits/${habitId}/logs?limit=20`);
        const logsContainer = document.getElementById("logsContainer");

        if (logs.length === 0) {
            logsContainer.innerHTML = '<div class="no-logs">No logs yet</div>';
            return;
        }

        logsContainer.innerHTML = logs
            .reverse()
            .map(
                (log) => `
            <div class="log-item">
                <span class="log-item-date">${log.date}</span>
                <button class="log-item-delete" data-log-id="${log.id}" title="Delete log">
                    ×
                </button>
            </div>
        `
            )
            .join("");

        logsContainer.querySelectorAll(".log-item-delete").forEach((btn) => {
            btn.addEventListener("click", (e) => {
                const logId = parseInt(btn.dataset.logId);
                deleteHabitLog(habitId, logId);
            });
        });
    } catch (error) {
        toast.error(`Failed to load logs: ${error.message}`);
    }
}

// ====================================================================
// HABIT ACTIONS
// ====================================================================

async function markHabitDone(habitId, btnElement = null) {
    try {
        const today = new Date().toISOString().split("T")[0];

        if (btnElement) {
            btnElement.disabled = true;
            btnElement.innerHTML = '<span class="loading-spinner"></span> Saving...';
        }

        await apiRequest("POST", `/habits/${habitId}/logs`, {
            date: today,
            notes: "",
        });

        toast.success("✓ Habit marked as done! Keep it up! 🎉");

        if (appState.selectedHabitId === habitId) {
            await showHabitDetails(habitId);
        } else {
            await loadHabits();
        }
    } catch (error) {
        if (error.status === 409 || error.message.includes("already exists")) {
            toast.warning("Already logged for today!");
        } else {
            toast.error(`Failed to log habit: ${error.message}`);
        }
    } finally {
        if (btnElement) {
            btnElement.disabled = false;
            btnElement.innerHTML = "✓ Done Today";
        }
    }
}

async function deleteHabit(habitId) {
    const habit = appState.habits.find((h) => h.id === habitId);
    const confirmed = await showConfirmDialog(
        "Delete Habit?",
        `Are you sure you want to delete "${habit.name}"? This action cannot be undone.`
    );

    if (!confirmed) return;

    try {
        await apiRequest("DELETE", `/habits/${habitId}`);
        toast.success("Habit deleted");

        document.getElementById("detailsSection").classList.add("hidden");
        appState.selectedHabitId = null;

        await loadHabits();
    } catch (error) {
        toast.error(`Failed to delete habit: ${error.message}`);
    }
}

async function deleteHabitLog(habitId, logId) {
    const confirmed = await showConfirmDialog(
        "Delete Log?",
        "Remove this completion record?"
    );

    if (!confirmed) return;

    try {
        await apiRequest("DELETE", `/habits/${habitId}/logs/${logId}`);
        toast.success("Log deleted");
        await loadHabitLogs(habitId);
    } catch (error) {
        toast.error(`Failed to delete log: ${error.message}`);
    }
}

// ====================================================================
// CREATE HABIT
// ====================================================================

function initCreateHabitForm() {
    const form = document.getElementById("createHabitForm");
    const nameInput = document.getElementById("habitName");
    const descInput = document.getElementById("habitDescription");
    const freqSelect = document.getElementById("habitFrequency");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = nameInput.value.trim();
        const description = descInput.value.trim();
        const frequency = freqSelect.value;

        if (!name || !frequency) {
            toast.error("Please fill in required fields");
            return;
        }

        const submitBtn = form.querySelector('button[type="submit"]');

        try {
            submitBtn.disabled = true;
            submitBtn.innerHTML =
                '<span class="loading-spinner"></span> Creating...';

            await apiRequest("POST", "/habits", {
                name,
                description,
                frequency,
            });

            toast.success(`✨ "${name}" created!`);
            form.reset();
            freqSelect.value = "";
            await loadHabits();
        } catch (error) {
            toast.error(`Failed to create habit: ${error.message}`);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = "➕ Create Habit";
        }
    });
}

// ====================================================================
// SEARCH
// ====================================================================

function initSearch() {
    const searchInput = document.getElementById("searchHabits");

    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.toLowerCase();

        appState.filteredHabits = appState.habits.filter((habit) =>
            habit.name.toLowerCase().includes(query) ||
            (habit.description && habit.description.toLowerCase().includes(query))
        );

        renderHabits();
    });
}

// ====================================================================
// HABIT SELECT DROPDOWN (OPTIONAL)
// ====================================================================

function updateHabitSelect() {
    // This function is a no-op for the modern UI
    // The old code referenced a habitSelect dropdown that's no longer used
    // Keeping it here for backwards compatibility
}

// ====================================================================
// WEEKLY SUMMARY
// ====================================================================

function initWeeklySummary() {
    const weekInput = document.getElementById("weekInput");
    const weeklySummary = document.getElementById("weeklySummary");

    // Load current week
    const today = new Date();
    const weekNum = getISOWeekNumber(today);
    const year = today.getFullYear();
    const defaultWeek = `${year}-${String(weekNum).padStart(2, "0")}`;
    weekInput.value = defaultWeek;

    // Load on input change
    weekInput.addEventListener("change", () => {
        loadWeeklySummary();
    });

    weekInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            loadWeeklySummary();
        }
    });

    // Initial load
    loadWeeklySummary();
}

async function loadWeeklySummary() {
    const weekInput = document.getElementById("weekInput");
    const weeklySummary = document.getElementById("weeklySummary");
    const week = weekInput.value.trim();

    if (!week) {
        weeklySummary.innerHTML =
            '<div class="weekly-empty">Enter a week to view summary</div>';
        return;
    }

    try {
        const summary = await apiRequest(
            "GET",
            `/analytics/weekly-summary?week=${encodeURIComponent(week)}`
        );

        if (summary.items.length === 0) {
            weeklySummary.innerHTML =
                '<div class="weekly-empty">No habits for this week</div>';
            return;
        }

        const html = `
            <table class="weekly-table">
                <thead>
                    <tr>
                        <th>Habit</th>
                        <th>Completions</th>
                    </tr>
                </thead>
                <tbody>
                    ${summary.items
                        .map(
                            (item) => `
                        <tr>
                            <td>${escapeHtml(item.habit_name)}</td>
                            <td class="weekly-completion">${item.completions}</td>
                        </tr>
                    `
                        )
                        .join("")}
                    <tr style="font-weight: 600; background: var(--bg-secondary);">
                        <td>Total Completions</td>
                        <td class="weekly-completion">${summary.total_completions}</td>
                    </tr>
                </tbody>
            </table>
        `;

        weeklySummary.innerHTML = html;
    } catch (error) {
        weeklySummary.innerHTML = `<div class="weekly-empty" style="color: var(--danger);">Error: ${escapeHtml(error.message)}</div>`;
    }
}

function getISOWeekNumber(date) {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

// ====================================================================
// UTILITIES
// ====================================================================

function escapeHtml(text) {
    if (!text) return "";
    const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
}

// ====================================================================
// INITIALIZATION
// ====================================================================

document.addEventListener("DOMContentLoaded", () => {
    // Initialize all components
    initApiKeyModal();
    initCreateHabitForm();
    initSearch();
    initWeeklySummary();

    // Load initial data
    loadHabits();

    // Close modals on Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            ModalManager.closeAll();
        }
    });

    // Close modals on background click
    document.querySelectorAll(".modal").forEach((modal) => {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) {
                ModalManager.close(modal);
            }
        });
    });
});
