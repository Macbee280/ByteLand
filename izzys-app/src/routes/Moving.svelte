<!-- ObjectMover.svelte -->
<script>
    let x = 100;
    let y = 100;
  
    window.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowUp') y -= 10;
      if (event.key === 'ArrowDown') y += 10;
      if (event.key === 'ArrowLeft') x -= 10;
      if (event.key === 'ArrowRight') x += 10;
    });
  </script>
  
  <div
    class="object"
    style="left: {x}px; top: {y}px;"
  ></div>
  