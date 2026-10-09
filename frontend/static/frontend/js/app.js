/*
    PaySecure
    Common Frontend JavaScript
*/


/* ==============================
   Authentication
============================== */

function getAccessToken() {

    return localStorage.getItem(
        "access_token"
    );
}


function getRefreshToken() {

    return localStorage.getItem(
        "refresh_token"
    );
}


function redirectToLogin() {

    window.location.href =
        "/login/";
}


/* ==============================
   API Helper
============================== */

async function apiFetch(
    url,
    options = {}
) {

    const token =
        getAccessToken();


    const headers = {
        "Content-Type":
            "application/json",

        ...(options.headers || {})
    };


    if (token) {

        headers["Authorization"] =
            `Bearer ${token}`;
    }


    const response =
        await fetch(
            url,
            {
                ...options,
                headers: headers
            }
        );


    /*
        If access token has expired,
        try refreshing it.
    */

    if (
        response.status === 401 &&
        getRefreshToken()
    ) {

        const refreshed =
            await refreshAccessToken();


        if (refreshed) {

            headers["Authorization"] =
                `Bearer ${getAccessToken()}`;


            return fetch(
                url,
                {
                    ...options,
                    headers: headers
                }
            );
        }
    }


    return response;
}


/* ==============================
   Refresh Token
============================== */

async function refreshAccessToken() {

    const refresh =
        getRefreshToken();


    if (!refresh) {

        return false;
    }


    try {

        const response =
            await fetch(
                "/api/token/refresh/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        refresh: refresh
                    })
                }
            );


        if (!response.ok) {

            clearAuth();

            return false;
        }


        const data =
            await response.json();


        localStorage.setItem(
            "access_token",
            data.access
        );


        return true;

    } catch (error) {

        clearAuth();

        return false;
    }
}


/* ==============================
   Logout
============================== */

async function logoutUser() {

    const refresh =
        getRefreshToken();


    try {

        if (refresh) {

            await apiFetch(
                "/api/accounts/logout/",
                {
                    method: "POST",

                    body: JSON.stringify({
                        refresh: refresh
                    })
                }
            );
        }

    } catch (error) {

        console.error(error);

    } finally {

        clearAuth();

        window.location.href =
            "/login/";
    }
}


function clearAuth() {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "refresh_token"
    );
}


/* ==============================
   Toast Notifications
============================== */

function showToast(
    message,
    type = "success"
) {

    const toast =
        document.getElementById(
            "toast"
        );


    if (!toast) {

        return;
    }


    toast.textContent =
        message;


    toast.className =
        `toast show ${type}`;


    setTimeout(() => {

        toast.className =
            "toast";

    }, 3500);
}


/* ==============================
   API Error
============================== */

function getApiError(data) {

    if (!data) {
        return "Something went wrong.";
    }

    // FastAPI / DRF detail message
    if (typeof data.detail === "string") {
        return data.detail;
    }

    if (data.message) {
        return data.message;
    }

    // Django serializer validation errors
    if (typeof data === "object") {

        const messages = [];

        Object.keys(data).forEach(field => {

            const errors = data[field];

            if (Array.isArray(errors)) {

                errors.forEach(error => {

                    messages.push(
                        `${field}: ${error}`
                    );

                });

            } else {

                messages.push(
                    `${field}: ${errors}`
                );
            }

        });

        if (messages.length) {

            return messages.join(" | ");
        }
    }

    return "Something went wrong.";
}

/* ==============================
   Formatting
============================== */

function formatAmount(amount) {

    const value =
        Number(amount || 0);


    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR"
        }
    ).format(value);
}


function formatDate(dateValue) {

    if (!dateValue) {

        return "-";
    }


    const date =
        new Date(dateValue);


    if (Number.isNaN(date.getTime())) {

        return dateValue;
    }


    return date.toLocaleDateString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    );
}


function getStatusClass(status) {

    if (status === "SUCCESS") {

        return "status-success";
    }


    if (status === "FAILED") {

        return "status-failed";
    }


    if (status === "PENDING") {

        return "status-pending";
    }


    return "";
}


/* ==============================
   Sidebar
============================== */

function toggleSidebar() {

    const sidebar =
        document.getElementById(
            "sidebar"
        );


    if (sidebar) {

        sidebar.classList.toggle(
            "open"
        );
    }
}


/* ==============================
   Card Number Formatting
============================== */

document.addEventListener(
    "input",
    function(event) {

        if (
            event.target.id ===
            "cardNumber"
        ) {

            let value =
                event.target.value
                    .replace(/\D/g, "")
                    .substring(0, 16);


            value =
                value.match(
                    /.{1,4}/g
                )?.join(" ") || "";


            event.target.value =
                value;
        }


        if (
            event.target.id ===
            "expiryDate"
        ) {

            let value =
                event.target.value
                    .replace(/\D/g, "")
                    .substring(0, 4);


            if (value.length >= 3) {

                value =
                    value.substring(0, 2)
                    + "/"
                    + value.substring(2);
            }


            event.target.value =
                value;
        }

    }
);


/* ==============================
   Active Navigation
============================== */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        const currentPath =
            window.location.pathname;


        document
            .querySelectorAll(".nav-link")
            .forEach(link => {

                const href =
                    link.getAttribute("href");


                if (
                    href &&
                    currentPath.startsWith(
                        href
                    ) &&
                    href !== "/"
                ) {

                    link.classList.add(
                        "active"
                    );
                }

            });

    }
);