backgroundColor: data.map(d => d.link === 'Up'
    ? (d.snr < 10 ? 'orange' : 'green')
    : 'red')
