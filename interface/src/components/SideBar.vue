<script setup lang="ts"></script>
<template>
  <aside class="w-72" aria-label="Sidebar">
    <div
      class="h-screen w-60 overflow-y-auto py-4 px-3 bg-gray-50 rounded dark:bg-gray-800"
    >
      <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white"
        >Crypto-Forecast</span
      >
      <ul class="space-y-2 pt-4">
        <li>
          <RouterLink
            to="/"
            class="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"
              />
            </svg>
            <span class="ml-3">Home</span>
          </RouterLink>
        </li>
        <li>
          <RouterLink
            to="/about"
            class="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <svg
              class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path>
              <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path>
            </svg>
            <span class="ml-3">Sentiment Analysis</span>
          </RouterLink>
        </li>
      </ul>
    </div>
  </aside>
</template>
<style></style>
