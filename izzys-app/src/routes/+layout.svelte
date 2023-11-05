<script>
    let message = "Hello, SvelteKit!";
  </script>
  
  <slot />

  <header>
    <h1>{message}</h1>
  </header>

  <style> /*if include :global() it will turn all stuff red, otherwise just */
    h1 {
      color: red;
    }
  </style>