import React, {useEffect, useState} from 'react';
import {BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Title, Tooltip,} from 'chart.js';
import {Bar} from "react-chartjs-2";
import './BarCovidChart.css';
import {Multiselect} from "multiselect-react-dropdown";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

export const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'bottom',
        },
        title: {
            display: true,
            text: 'Corona Virus Country wise data'
        },
    },
};


const checkbox_list = {
    'total_cases': 'Total Cases',
    'total_deaths': 'Total Deaths',
    'total_recovered': 'Total Recovered',
    'active_cases': 'Active Cases',
    'total_tests_1m_pop': 'Total Cases/1M',
    'deaths_1m_pop': 'Total Deaths/1M',
    'total_tests': 'Total Tests',
    'tests_1m_pop': 'Total Tests/1M',
    'population': 'Population',
}


export function BarCovidChart() {

    let data = {
        labels: [],
        datasets: [],
    };


    const [result, setResult] = useState([]);
    const [chartData, setChartData] = useState(data);
    const [checkboxValue, setCheckboxValue] = useState(data);

    useEffect(() => {
        const url = "https://lucid-destiny-367614.wn.r.appspot.com/api/v1/countries", fetchData = async () => {
            try {
                const response = await fetch(url);
                const json = await response.json();
                setResult(json);
                setChartData({
                    labels: json.map((country) => country.country).slice(0, 10),
                    datasets: chartData.datasets
                });
            } catch (error) {
                console.log("error", error);
            }
        };

        fetchData().then(r => console.log("done"));
    }, []);

    function updateCountryChartData(selectedList) {
        setChartData({
            ...chartData,
            labels: result.filter((country) => selectedList.find((item) => item === country.country)).map((country) => country.country),
            datasets: chartData.datasets.map((dataset) => {
                return {
                    ...dataset,
                    data: result.filter((country) => selectedList.includes(country.country)).map((country) => country[dataset.label.toLowerCase()]),
                }
            })
        })
    }

    const updateChart = (event) => {
            // data: result.map((country) => selectedCountryList.find((item) => item === country.country)),

            const {checked, name: selected_checkbox} = event.target;
            setCheckboxValue({...checkboxValue, [selected_checkbox]: checked});
            if (checked) {
                setChartData({
                    ...chartData,
                    datasets: [
                        ...chartData.datasets, {
                            data: result.map((country) => country[selected_checkbox]),
                            label: checkbox_list[selected_checkbox],
                            backgroundColor: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.5)`,
                        }]
                })
            } else {
                setChartData({
                    ...chartData,
                    datasets: chartData.datasets.filter((dataset) => dataset.label !== checkbox_list[selected_checkbox])
                })
            }
        }, selectedCountry = (selectedCountryList) => updateCountryChartData(selectedCountryList),
        removedCountry = (selectedList) => updateCountryChartData(selectedList);


    return (
        <div>
            <Multiselect className={"multiselect"}
                         options={result.map((country) => country.country)}
                         displayValue="key"
                         onSelect={selectedCountry}
                         onRemove={removedCountry}
                         showCheckbox={true}
                         isObject={false}
            />

            <div className='row'>
                {Object.keys(checkbox_list).map((key) => {
                    return <div>
                        <input onChange={updateChart}
                               type="checkbox" id={key} name={key} value={key} className={'checkbox'}/>

                        <label form={key}>{checkbox_list[key]}</label>
                    </div>
                })
                }
            </div>
            <div className={'give-spacing'}><Bar options={options} data={chartData}/>
            </div>
        </div>
    );
}

export default BarCovidChart;
